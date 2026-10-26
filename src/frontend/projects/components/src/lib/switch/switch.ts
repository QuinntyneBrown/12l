import { ChangeDetectionStrategy, Component, booleanAttribute, input, model } from '@angular/core';

/**
 * An on or off setting: a native checkbox with role="switch" and a visually hidden label naming
 * the setting (design system: Switch). A locked setting is checked and disabled.
 */
@Component({
  selector: 'tl-switch',
  templateUrl: './switch.html',
  styleUrl: './switch.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SwitchComponent {
  readonly label = input.required<string>();
  readonly checked = model(false);
  readonly disabled = input(false, { transform: booleanAttribute });
}
