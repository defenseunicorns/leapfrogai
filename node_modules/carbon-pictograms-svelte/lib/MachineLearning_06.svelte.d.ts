import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MachineLearning_06Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MachineLearning_06 extends SvelteComponentTyped<
  MachineLearning_06Props,
  Record<string, any>,
  {}
> {}
