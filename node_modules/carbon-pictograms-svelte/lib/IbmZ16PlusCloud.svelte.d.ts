import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface IbmZ16PlusCloudProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class IbmZ16PlusCloud extends SvelteComponentTyped<
  IbmZ16PlusCloudProps,
  Record<string, any>,
  {}
> {}
