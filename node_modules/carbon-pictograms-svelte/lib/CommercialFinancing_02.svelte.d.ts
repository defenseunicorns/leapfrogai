import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface CommercialFinancing_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class CommercialFinancing_02 extends SvelteComponentTyped<
  CommercialFinancing_02Props,
  Record<string, any>,
  {}
> {}
