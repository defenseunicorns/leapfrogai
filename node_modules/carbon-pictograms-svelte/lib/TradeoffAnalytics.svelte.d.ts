import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface TradeoffAnalyticsProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class TradeoffAnalytics extends SvelteComponentTyped<
  TradeoffAnalyticsProps,
  Record<string, any>,
  {}
> {}
