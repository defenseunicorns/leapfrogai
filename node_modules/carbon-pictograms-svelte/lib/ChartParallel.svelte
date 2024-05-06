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
  <path d="M31.36,31h-0.72V18.809l-9.28,8.351V31h-0.72v-3.827l-9.28-7.424V31h-0.72V19.869l-9.28,9.28V31	H0.64V1h0.72v6.468l9.28-3.712V1h0.72v2.756l9.28,3.712V1h0.721v6.417l9.279-4.64V1h0.721L31.36,31L31.36,31z M1.36,18.173v9.958	l9.28-9.28v-8.102L1.36,18.173z M11.36,18.827l9.28,7.424v-6.102l-9.28-9.28V18.827z M21.36,20.14v6.052l9.279-8.352V9.931	L21.36,20.14z M11.36,9.851l9.28,9.28V8.244l-9.28-3.712V9.851z M21.36,8.223v10.846l9.28-10.208V3.583L21.36,8.223z M1.36,8.244	v9.007l9.28-7.424V4.532L1.36,8.244z"></path>
</svg>