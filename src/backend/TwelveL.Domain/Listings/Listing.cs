namespace TwelveL.Domain.Listings;

/// <summary>Lifecycle states of a listing (L2-019).</summary>
public enum ListingStatus
{
    Draft,
    Active,
    Reserved,
    Sold,
    Removed,
}

/// <summary>The editable fields of a listing as a client sends them. Every field but the category may be missing in a draft.</summary>
public sealed record ListingDetails(
    string? Category,
    string? Subcategory,
    string? Size,
    string? Title,
    string? Description,
    string? Brand,
    string? Condition,
    string? Flaws,
    decimal? Price,
    decimal? ShippingCost)
{
    public static readonly ListingDetails Empty = new(null, null, null, null, null, null, null, null, null, null);
}

/// <summary>One broken listing rule: the request field, a stable code and the message the form shows.</summary>
public sealed record RuleViolation(string Field, string Code, string Message);

/// <summary>
/// One item offered for sale by one seller. The size has no public setter: it is always set from
/// the category (L2-013). This feature owns (new) → Draft and Draft → Active.
/// </summary>
public sealed class Listing
{
    public const int MaxTitle = 80;
    public const int MinTitle = 5;
    public const int MaxDescription = 2000;
    public const int MinDescription = 20;
    public const int MaxBrand = 50;
    public const int MaxFlaws = 500;
    public const int MinFlaws = 10;
    public const decimal MinPrice = 1.00m;
    public const decimal MaxPrice = 5000.00m;
    public const decimal MaxShipping = 100.00m;

    private Listing()
    {
    }

    public Guid Id { get; private set; }

    /// <summary>Sequential public number; the reference is "L-" followed by it.</summary>
    public long Number { get; private set; }

    public string Reference { get; private set; } = string.Empty;

    public Guid SellerId { get; private set; }

    public ListingStatus Status { get; private set; }

    public string Category { get; private set; } = string.Empty;

    public string? Subcategory { get; private set; }

    public string Size { get; private set; } = string.Empty;

    public string? Title { get; private set; }

    public string? Description { get; private set; }

    public string? Brand { get; private set; }

    public ItemCondition? Condition { get; private set; }

    public string? Flaws { get; private set; }

    public decimal? Price { get; private set; }

    public decimal? ShippingCost { get; private set; }

    public DateTime? SizeConfirmedAt { get; private set; }

    public DateTime CreatedAt { get; private set; }

    public DateTime UpdatedAt { get; private set; }

    public DateTime? PublishedAt { get; private set; }

    public static string ReferenceFor(long number) => $"L-{number}";

    /// <summary>Creates a draft. Call <see cref="CheckDraft"/> first; the category must be accepted.</summary>
    public static Listing CreateDraft(Guid sellerId, long number, ListingDetails details, DateTime now)
    {
        var listing = new Listing
        {
            Id = Guid.NewGuid(),
            Number = number,
            Reference = ReferenceFor(number),
            SellerId = sellerId,
            Status = ListingStatus.Draft,
            CreatedAt = now,
        };
        listing.UpdateDetails(details, now);
        return listing;
    }

    /// <summary>Replaces the editable fields, trimming text and setting the size from the category.</summary>
    public void UpdateDetails(ListingDetails details, DateTime now)
    {
        Category = details.Category ?? throw new ArgumentException("A listing needs a category.", nameof(details));
        Size = CategoryCatalog.AcceptedSizeFor(Category);
        Subcategory = Clean(details.Subcategory);
        Title = Clean(details.Title);
        Description = Clean(details.Description);
        Brand = Clean(details.Brand);
        Condition = ItemConditions.FromLabel(details.Condition);
        Flaws = Condition == ItemCondition.UsedFair ? Clean(details.Flaws) : null;
        Price = details.Price;
        ShippingCost = details.ShippingCost;
        UpdatedAt = now;
    }

    /// <summary>Draft rules (L2-019): an accepted category and size, and every present field within its limits.</summary>
    public static IReadOnlyList<RuleViolation> CheckDraft(ListingDetails details)
    {
        var violations = new List<RuleViolation>();
        var category = CategoryCatalog.Find(details.Category);
        if (category is null)
        {
            violations.Add(new("category", "CATEGORY_INVALID", "Choose a category"));
        }
        else if (Clean(details.Subcategory) is { } subcategory && !category.Subcategories.Contains(subcategory))
        {
            violations.Add(new("subcategory", "CATEGORY_INVALID", "Choose a type for this category"));
        }

        if (category is not null && Clean(details.Size) is { } size && !string.Equals(size, category.AcceptedSize, StringComparison.OrdinalIgnoreCase))
        {
            violations.Add(new("size", "SIZE_NOT_ACCEPTED", $"12L accepts only {category.AcceptedSize.ToLowerInvariant()} in {category.Name}"));
        }

        if (Clean(details.Title)?.Length > MaxTitle)
        {
            violations.Add(TitleLength);
        }

        if (Clean(details.Description)?.Length > MaxDescription)
        {
            violations.Add(DescriptionLength);
        }

        if (Clean(details.Brand)?.Length > MaxBrand)
        {
            violations.Add(BrandLength);
        }

        if (details.Condition is not null && ItemConditions.FromLabel(details.Condition) is null)
        {
            violations.Add(new("condition", "CONDITION_INVALID", "Choose one of the 5 conditions"));
        }

        if (Clean(details.Flaws)?.Length > MaxFlaws)
        {
            violations.Add(new("flaws", "FLAWS_LENGTH", $"Keep the flaws to {MaxFlaws} characters"));
        }

        if (details.Price is { } price && !IsMoney(price, MinPrice, MaxPrice))
        {
            violations.Add(PriceOutOfRange);
        }

        if (details.ShippingCost is { } shipping && !IsMoney(shipping, 0m, MaxShipping))
        {
            violations.Add(ShippingOutOfRange);
        }

        return violations;
    }

    /// <summary>
    /// Publishes a draft when the publish rules of L2-014 to L2-018 hold, reporting every failing
    /// field together; otherwise leaves it unchanged.
    /// </summary>
    public IReadOnlyList<RuleViolation> Publish(bool sizeConfirmed, DateTime now)
    {
        if (Status != ListingStatus.Draft)
        {
            throw new InvalidOperationException("Only a draft can be published.");
        }

        var details = new ListingDetails(Category, Subcategory, Size, Title, Description, Brand, Condition?.ToLabel(), Flaws, Price, ShippingCost);
        var draft = CheckDraft(details).ToDictionary(v => v.Field);
        var violations = new List<RuleViolation>();
        void Check(string field, bool failed, RuleViolation violation)
        {
            if (draft.TryGetValue(field, out var existing))
            {
                violations.Add(existing);
            }
            else if (failed)
            {
                violations.Add(violation);
            }
        }

        Check("subcategory", Subcategory is null, new("subcategory", "SUBCATEGORY_REQUIRED", "Choose a type"));
        Check("title", Title is null || Title.Length < MinTitle, TitleLength);
        Check("description", Description is null || Description.Length < MinDescription, DescriptionLength);
        Check("brand", Brand is null, BrandLength);
        Check("condition", Condition is null, new("condition", "CONDITION_REQUIRED", "Choose a condition"));
        if (Condition == ItemCondition.UsedFair)
        {
            Check("flaws", Flaws is null || Flaws.Length < MinFlaws, new("flaws", "FLAWS_REQUIRED", "Describe the item's flaws"));
        }

        Check("price", Price is null, PriceOutOfRange);
        Check("shippingCost", ShippingCost is null, ShippingOutOfRange);
        if (!sizeConfirmed)
        {
            var label = Size == CategoryCatalog.MensUs12 ? "men's US 12" : "men's L";
            violations.Add(new("sizeConfirmed", "SIZE_CONFIRMATION_REQUIRED", $"Confirm the label shows {label}"));
        }

        if (violations.Count == 0)
        {
            Status = ListingStatus.Active;
            SizeConfirmedAt = now;
            PublishedAt ??= now;
            UpdatedAt = now;
        }

        return violations;
    }

    private static readonly RuleViolation TitleLength = new("title", "TITLE_LENGTH", "Title must be 5 to 80 characters");
    private static readonly RuleViolation DescriptionLength = new("description", "DESCRIPTION_LENGTH", "Description must be 20 to 2,000 characters");
    private static readonly RuleViolation BrandLength = new("brand", "BRAND_LENGTH", "Brand must be 1 to 50 characters");
    private static readonly RuleViolation PriceOutOfRange = new("price", "PRICE_OUT_OF_RANGE", "Enter a price from $1.00 to $5,000.00");
    private static readonly RuleViolation ShippingOutOfRange = new("shippingCost", "SHIPPING_OUT_OF_RANGE", "Enter shipping from $0.00 to $100.00");

    private static bool IsMoney(decimal value, decimal min, decimal max) =>
        value >= min && value <= max && decimal.Round(value, 2) == value;

    private static string? Clean(string? value) => string.IsNullOrWhiteSpace(value) ? null : value.Trim();
}
