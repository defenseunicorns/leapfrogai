import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface RedefiningFinancialServicesProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class RedefiningFinancialServices extends SvelteComponentTyped<
  RedefiningFinancialServicesProps,
  Record<string, any>,
  {}
> {}
