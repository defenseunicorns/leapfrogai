import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface ManageApplicationsAnywhereProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class ManageApplicationsAnywhere extends SvelteComponentTyped<
  ManageApplicationsAnywhereProps,
  Record<string, any>,
  {}
> {}
