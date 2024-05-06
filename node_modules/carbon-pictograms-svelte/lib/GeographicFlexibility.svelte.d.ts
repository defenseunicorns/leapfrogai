import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface GeographicFlexibilityProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class GeographicFlexibility extends SvelteComponentTyped<
  GeographicFlexibilityProps,
  Record<string, any>,
  {}
> {}
