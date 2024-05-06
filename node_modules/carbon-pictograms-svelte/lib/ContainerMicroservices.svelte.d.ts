import type { SvelteComponentTyped } from "svelte";
import type { SvelteHTMLElements } from "svelte/elements";

type RestProps = SvelteHTMLElements["svg"];

export interface ContainerMicroservicesProps extends RestProps {
  /**
   * Specify the pictogram title.
   * @default undefined
   */
  title?: string;

  [key: `data-${string}`]: any;
}

export default class ContainerMicroservices extends SvelteComponentTyped<
  ContainerMicroservicesProps,
  Record<string, any>,
  {}
> {}
