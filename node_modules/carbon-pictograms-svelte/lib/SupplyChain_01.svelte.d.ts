import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface SupplyChain_01Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class SupplyChain_01 extends SvelteComponentTyped<
  SupplyChain_01Props,
  Record<string, any>,
  {}
> {}
