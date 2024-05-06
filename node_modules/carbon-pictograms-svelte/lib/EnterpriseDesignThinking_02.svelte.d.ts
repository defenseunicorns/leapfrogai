import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface EnterpriseDesignThinking_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class EnterpriseDesignThinking_02 extends SvelteComponentTyped<
  EnterpriseDesignThinking_02Props,
  Record<string, any>,
  {}
> {}
