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
  <path d="M30.509,23l-4.254,4.255l-0.51-0.51l3.386-3.385H18c-1.577,0-2.86-1.283-2.86-2.86	s1.283-2.86,2.86-2.86h2.033v0.721H18c-1.18,0-2.14,0.96-2.14,2.14s0.96,2.14,2.14,2.14h11.131l-3.386-3.385l0.51-0.51L30.509,23z M12.36,4.532L16,2.417l11.64,6.79V15h0.721V9c0-0.128-0.068-0.247-0.179-0.311l-12-7c-0.111-0.065-0.25-0.065-0.362,0l-4,2.325	c-0.111,0.064-0.179,0.183-0.179,0.311V13h0.72V4.532H12.36z M8.36,6H7.64v10h0.72V6z M4.36,9H3.64v14	c0,0.128,0.068,0.246,0.179,0.311l12,7l0.362-0.621L4.36,22.793V9z"></path>
</svg>