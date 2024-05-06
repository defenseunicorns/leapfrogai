import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface ErlenmeyerFlaskProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class ErlenmeyerFlask extends SvelteComponentTyped<
  ErlenmeyerFlaskProps,
  Record<string, any>,
  {}
> {}
