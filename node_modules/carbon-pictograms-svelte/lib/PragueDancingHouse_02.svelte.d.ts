import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface PragueDancingHouse_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class PragueDancingHouse_02 extends SvelteComponentTyped<
  PragueDancingHouse_02Props,
  Record<string, any>,
  {}
> {}
