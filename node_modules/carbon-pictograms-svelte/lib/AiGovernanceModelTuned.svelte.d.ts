import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface AiGovernanceModelTunedProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class AiGovernanceModelTuned extends SvelteComponentTyped<
  AiGovernanceModelTunedProps,
  Record<string, any>,
  {}
> {}
