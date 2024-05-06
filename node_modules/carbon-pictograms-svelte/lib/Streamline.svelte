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
  <path d="M8.5,26.36c-1.577,0-2.86-1.283-2.86-2.86v-15c0-1.18-0.96-2.14-2.14-2.14S1.36,7.32,1.36,8.5V11H0.64	V8.5c0-1.577,1.283-2.86,2.86-2.86S6.36,6.923,6.36,8.5v15c0,1.18,0.96,2.14,2.14,2.14s2.14-0.96,2.14-2.14v-11	c0-1.577,1.283-2.86,2.86-2.86s2.86,1.283,2.86,2.86v7c0,1.18,0.96,2.14,2.14,2.14s2.14-0.96,2.14-2.14v-1	c0-1.577,1.283-2.86,2.86-2.86h6.631l-2.386-2.386l0.51-0.509L31.509,16l-3.254,3.255l-0.51-0.51l2.386-2.385H23.5	c-1.18,0-2.14,0.96-2.14,2.14v1c0,1.577-1.283,2.86-2.86,2.86s-2.86-1.283-2.86-2.86v-7c0-1.18-0.96-2.14-2.14-2.14	s-2.14,0.96-2.14,2.14v11C11.36,25.077,10.077,26.36,8.5,26.36z"></path>
</svg>