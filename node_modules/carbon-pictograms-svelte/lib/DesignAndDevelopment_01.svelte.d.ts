import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface DesignAndDevelopment_01Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class DesignAndDevelopment_01 extends SvelteComponentTyped<
  DesignAndDevelopment_01Props,
  Record<string, any>,
  {}
> {}
