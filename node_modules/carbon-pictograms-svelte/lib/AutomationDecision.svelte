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
  <path d="M27.255,19.255L30.509,16l-3.254-3.254l-0.51,0.509l2.386,2.386H16.149L9.36,8.85V5.36h19.771	l-2.386,2.386l0.51,0.509L30.509,5l-3.254-3.254l-0.51,0.509l2.386,2.386H9C8.801,4.64,8.64,4.801,8.64,5v3.85l-6.895,6.896	c-0.141,0.141-0.141,0.368,0,0.509L8.64,23.15V27c0,0.199,0.161,0.36,0.36,0.36h20.131l-2.386,2.385l0.51,0.51L30.509,27	l-3.254-3.255l-0.51,0.51l2.386,2.385H9.36v-3.49l6.789-6.79h12.982l-2.386,2.385L27.255,19.255z M9,22.491L2.509,16L9,9.508	L15.491,16L9,22.491z"></path>
</svg>