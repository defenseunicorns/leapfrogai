import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface MexicoCityMuseoSoumayaProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class MexicoCityMuseoSoumaya extends SvelteComponentTyped<
  MexicoCityMuseoSoumayaProps,
  Record<string, any>,
  {}
> {}
