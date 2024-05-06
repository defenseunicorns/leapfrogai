import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface AmsterdamWindmillProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class AmsterdamWindmill extends SvelteComponentTyped<
  AmsterdamWindmillProps,
  Record<string, any>,
  {}
> {}
