import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface IbmZ16MultiFrameProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class IbmZ16MultiFrame extends SvelteComponentTyped<
  IbmZ16MultiFrameProps,
  Record<string, any>,
  {}
> {}
