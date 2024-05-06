import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface AdvancedFraudProtectionProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class AdvancedFraudProtection extends SvelteComponentTyped<
  AdvancedFraudProtectionProps,
  Record<string, any>,
  {}
> {}
