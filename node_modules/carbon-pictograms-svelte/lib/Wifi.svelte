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
  <path d="M16,27.86c-1.854,0-3.362-1.509-3.362-3.362s1.508-3.362,3.362-3.362s3.362,1.509,3.362,3.362	S17.854,27.86,16,27.86z M16,21.856c-1.457,0-2.642,1.185-2.642,2.642S14.543,27.14,16,27.14s2.642-1.185,2.642-2.642	S17.457,21.856,16,21.856z M22.896,18.477c-1.929-1.616-4.379-2.505-6.899-2.505c-2.518,0-4.966,0.888-6.894,2.501L8.642,17.92	c2.058-1.721,4.67-2.668,7.356-2.668c2.689,0,5.303,0.949,7.362,2.672L22.896,18.477z M26.827,14.531	c-2.985-2.654-6.831-4.116-10.831-4.116c-3.996,0-7.84,1.46-10.825,4.111l-0.479-0.538c3.117-2.768,7.131-4.292,11.303-4.292	c4.175,0,8.192,1.526,11.309,4.298L26.827,14.531z M30.757,10.594C26.719,6.896,21.478,4.86,15.998,4.86	c-5.478,0-10.717,2.035-14.754,5.729l-0.486-0.531C4.927,6.242,10.34,4.14,15.998,4.14c5.66,0,11.075,2.103,15.246,5.922	L30.757,10.594z"></path>
</svg>