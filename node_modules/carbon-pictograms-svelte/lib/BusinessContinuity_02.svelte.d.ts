import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface BusinessContinuity_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class BusinessContinuity_02 extends SvelteComponentTyped<
  BusinessContinuity_02Props,
  Record<string, any>,
  {}
> {}
