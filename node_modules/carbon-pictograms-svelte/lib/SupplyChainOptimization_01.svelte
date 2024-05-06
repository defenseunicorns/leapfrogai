<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M10,31.36H2v-0.72h8V31.36z M11.36,30h-0.72v-8h0.72V30z M1.36,30H0.64v-8h0.72 V30z M20,21.36h-8v-0.72h8V21.36z M10,21.36H2v-0.72h8V21.36z M21.36,20h-0.72v-8h0.721L21.36,20L21.36,20z M11.36,20h-0.72v-8 h0.72V20z M15,18.36c-0.092,0-0.184-0.035-0.254-0.105l-2-2l0.509-0.509L15,17.491l3.745-3.746l0.51,0.509l-4,4 C15.184,18.325,15.092,18.36,15,18.36z M30,11.36h-8v-0.72h8V11.36z M20,11.36h-8v-0.72h8V11.36z M31.36,10h-0.72V2h0.721L31.36,10 L31.36,10z M21.36,10h-0.72V2h0.721L21.36,10L21.36,10z M30,1.36h-8V0.64h8V1.36z"></path>
</svg>