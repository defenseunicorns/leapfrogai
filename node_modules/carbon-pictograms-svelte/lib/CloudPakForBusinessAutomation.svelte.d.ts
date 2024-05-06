import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface CloudPakForBusinessAutomationProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class CloudPakForBusinessAutomation extends SvelteComponentTyped<
  CloudPakForBusinessAutomationProps,
  Record<string, any>,
  {}
> {}
