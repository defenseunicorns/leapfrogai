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
  <path d="M18.36,30h-0.72v-8.313c0-0.156,0.101-0.295,0.25-0.343c2.542-0.821,4.25-3.17,4.25-5.844	c0-3.386-2.754-6.14-6.14-6.14s-6.14,2.754-6.14,6.14c0,2.674,1.708,5.022,4.251,5.844c0.148,0.048,0.249,0.187,0.249,0.343V30	h-0.72v-8.057c-2.703-0.987-4.5-3.544-4.5-6.443c0-3.783,3.077-6.86,6.86-6.86c3.782,0,6.86,3.077,6.86,6.86	c0,2.899-1.798,5.456-4.5,6.443V30z M16,7.36c-1.577,0-2.86-1.283-2.86-2.86S14.423,1.64,16,1.64s2.86,1.283,2.86,2.86	S17.577,7.36,16,7.36z M16,2.36c-1.18,0-2.14,0.96-2.14,2.14S14.82,6.64,16,6.64s2.14-0.96,2.14-2.14S17.181,2.36,16,2.36z"></path>
</svg>