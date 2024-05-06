import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface NycManhattan_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class NycManhattan_02 extends SvelteComponentTyped<
  NycManhattan_02Props,
  Record<string, any>,
  {}
> {}
