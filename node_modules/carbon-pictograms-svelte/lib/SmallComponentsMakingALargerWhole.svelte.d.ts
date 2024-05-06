import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface SmallComponentsMakingALargerWholeProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class SmallComponentsMakingALargerWhole extends SvelteComponentTyped<
  SmallComponentsMakingALargerWholeProps,
  Record<string, any>,
  {}
> {}
