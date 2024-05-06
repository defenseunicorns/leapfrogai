import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MachineLearning_03Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MachineLearning_03 extends SvelteComponentTyped<
  MachineLearning_03Props,
  Record<string, any>,
  {}
> {}
