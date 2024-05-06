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
  <path d="M16,31.36	c-0.059,0-0.117-0.015-0.171-0.043l-13-7C2.713,24.254,2.64,24.133,2.64,24V8c0-0.132,0.073-0.254,0.189-0.317l13-7	c0.107-0.058,0.234-0.058,0.342,0l13,7C29.287,7.746,29.36,7.868,29.36,8v16c0,0.133-0.073,0.254-0.189,0.317l-13,7	C16.117,31.346,16.059,31.36,16,31.36z M16.36,22.714v7.684l12.28-6.612V8.603l-6.279,3.382v7.249c0,0.132-0.072,0.253-0.188,0.316	L16.36,22.714z M3.36,23.785l12.28,6.612v-7.684L9.828,19.55c-0.116-0.063-0.188-0.185-0.188-0.316v-7.249L3.36,8.603V23.785z M16.36,15.215v6.68l5.28-2.875v-6.647L16.36,15.215z M10.36,19.02l5.28,2.875v-6.68l-5.28-2.843	C10.36,12.372,10.36,19.02,10.36,19.02z M10.754,11.766L16,14.591l5.246-2.825L16,8.91L10.754,11.766z M16,8.14	c0.059,0,0.119,0.015,0.172,0.043l5.831,3.175L28.24,8L16,1.409L3.759,8l6.237,3.358l5.831-3.175C15.881,8.155,15.941,8.14,16,8.14z"></path>
</svg>