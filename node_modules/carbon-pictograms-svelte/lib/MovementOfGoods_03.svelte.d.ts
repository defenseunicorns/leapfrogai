import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MovementOfGoods_03Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MovementOfGoods_03 extends SvelteComponentTyped<
  MovementOfGoods_03Props,
  Record<string, any>,
  {}
> {}
