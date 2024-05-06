import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MovementOfGoods_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MovementOfGoods_02 extends SvelteComponentTyped<
  MovementOfGoods_02Props,
  Record<string, any>,
  {}
> {}
