import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface HybridCloud_03Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class HybridCloud_03 extends SvelteComponentTyped<
  HybridCloud_03Props,
  Record<string, any>,
  {}
> {}
