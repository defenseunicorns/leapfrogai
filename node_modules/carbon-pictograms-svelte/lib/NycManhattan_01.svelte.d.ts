import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface NycManhattan_01Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class NycManhattan_01 extends SvelteComponentTyped<
  NycManhattan_01Props,
  Record<string, any>,
  {}
> {}
