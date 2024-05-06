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
  <path d="M16.322,31.161l-0.644-0.322l4-8C19.74,22.717,19.864,22.64,20,22.64h7c2.007,0,3.64-1.633,3.64-3.64V5 c0-2.007-1.633-3.64-3.64-3.64H5C2.993,1.36,1.36,2.993,1.36,5v14c0,2.007,1.633,3.64,3.64,3.64h11v0.721H5 c-2.404,0-4.36-1.956-4.36-4.36V5c0-2.404,1.956-4.36,4.36-4.36h22c2.404,0,4.36,1.956,4.36,4.36v14c0,2.404-1.956,4.36-4.36,4.36 h-6.777L16.322,31.161z"></path><path d="M17.5,12.5c0,0.828-0.672,1.5-1.5,1.5c-0.828,0-1.5-0.672-1.5-1.5S15.172,11,16,11C16.828,11,17.5,11.672,17.5,12.5z M23.5,11c-0.828,0-1.5,0.672-1.5,1.5s0.672,1.5,1.5,1.5s1.5-0.672,1.5-1.5S24.328,11,23.5,11z M8.5,11C7.672,11,7,11.672,7,12.5 S7.672,14,8.5,14s1.5-0.672,1.5-1.5S9.328,11,8.5,11z"></path>
</svg>