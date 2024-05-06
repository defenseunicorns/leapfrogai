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
  <path d="M21.591,27.473L19.109,24h1.275l1.777,2.605h0.041	L24.047,24h1.207l-2.469,3.391L25.308,31h-1.275l-1.818-2.74h-0.041L20.208,31H19L21.591,27.473z M27.244,26.027v-0.613h1.1v-2.843	h-0.052l-0.871,1.032l-0.47-0.395l0.992-1.181h1.14v3.387H30v0.613C30,26.027,27.244,26.027,27.244,26.027z M16.36,31h-0.72V16.36	H9.433l-8.248,4.949l-0.37-0.617l7.219-4.332H1v-0.72h8.233l6.407-3.844V1h0.72v10.364l14.455-8.673l0.371,0.617L16.36,12.204v3.437	H31v0.72H16.36V31z M10.633,15.64h5.007v-3.004L10.633,15.64z"></path>
</svg>