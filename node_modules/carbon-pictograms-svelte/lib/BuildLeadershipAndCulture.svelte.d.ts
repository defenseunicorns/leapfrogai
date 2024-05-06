import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface BuildLeadershipAndCultureProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class BuildLeadershipAndCulture extends SvelteComponentTyped<
  BuildLeadershipAndCultureProps,
  Record<string, any>,
  {}
> {}
