import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MovementOfGoods_01Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MovementOfGoods_01 extends SvelteComponentTyped<
  MovementOfGoods_01Props,
  Record<string, any>,
  {}
> {}
