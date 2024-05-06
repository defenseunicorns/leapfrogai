import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface BuildAndDeployPipelineProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class BuildAndDeployPipeline extends SvelteComponentTyped<
  BuildAndDeployPipelineProps,
  Record<string, any>,
  {}
> {}
