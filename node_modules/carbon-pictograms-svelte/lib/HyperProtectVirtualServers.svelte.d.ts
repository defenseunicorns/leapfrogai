import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface HyperProtectVirtualServersProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class HyperProtectVirtualServers extends SvelteComponentTyped<
  HyperProtectVirtualServersProps,
  Record<string, any>,
  {}
> {}
