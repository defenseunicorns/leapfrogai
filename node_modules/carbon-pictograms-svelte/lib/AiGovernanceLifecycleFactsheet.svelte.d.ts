import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface AiGovernanceLifecycleFactsheetProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class AiGovernanceLifecycleFactsheet extends SvelteComponentTyped<
  AiGovernanceLifecycleFactsheetProps,
  Record<string, any>,
  {}
> {}
