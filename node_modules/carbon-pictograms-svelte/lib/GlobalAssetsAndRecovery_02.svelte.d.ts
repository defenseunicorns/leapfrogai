import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface GlobalAssetsAndRecovery_02Props extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class GlobalAssetsAndRecovery_02 extends SvelteComponentTyped<
  GlobalAssetsAndRecovery_02Props,
  Record<string, any>,
  {}
> {}
