import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface SystemsDevopsDeployProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class SystemsDevopsDeploy extends SvelteComponentTyped<
  SystemsDevopsDeployProps,
  Record<string, any>,
  {}
> {}
