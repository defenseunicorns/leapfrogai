import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface WashingtonDcMonumentProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class WashingtonDcMonument extends SvelteComponentTyped<
  WashingtonDcMonumentProps,
  Record<string, any>,
  {}
> {}
