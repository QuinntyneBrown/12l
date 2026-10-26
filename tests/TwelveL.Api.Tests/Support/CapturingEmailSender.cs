using System.Collections.Concurrent;
using TwelveL.Application.Abstractions;

namespace TwelveL.Api.Tests.Support;

/// <summary>Records every email instead of sending it.</summary>
public sealed class CapturingEmailSender : IEmailSender
{
    public ConcurrentQueue<EmailMessage> Sent { get; } = new();

    public Task SendAsync(EmailMessage message, CancellationToken cancellationToken)
    {
        Sent.Enqueue(message);
        return Task.CompletedTask;
    }

    /// <summary>The verification token from the last email sent to <paramref name="to"/>.</summary>
    public string LastVerificationToken(string to)
    {
        var message = Sent.Last(m => string.Equals(m.To, to, StringComparison.OrdinalIgnoreCase));
        var start = message.Body.IndexOf("token=", StringComparison.Ordinal) + "token=".Length;
        var end = message.Body.IndexOfAny([' ', '\n', '\r', '"'], start);
        return Uri.UnescapeDataString(end < 0 ? message.Body[start..] : message.Body[start..end]);
    }
}
