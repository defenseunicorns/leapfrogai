import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface ResetHybridCloudProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class ResetHybridCloud extends SvelteComponentTyped<
  ResetHybridCloudProps,
  Record<string, any>,
  {}
> {}
