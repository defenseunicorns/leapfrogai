import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface SupplyChainOptimization_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class SupplyChainOptimization_02 extends SvelteComponentTyped<
  SupplyChainOptimization_02Props,
  Record<string, any>,
  {}
> {}
