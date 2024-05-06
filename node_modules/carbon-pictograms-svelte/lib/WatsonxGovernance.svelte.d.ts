import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface WatsonxGovernanceProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class WatsonxGovernance extends SvelteComponentTyped<
  WatsonxGovernanceProps,
  Record<string, any>,
  {}
> {}
