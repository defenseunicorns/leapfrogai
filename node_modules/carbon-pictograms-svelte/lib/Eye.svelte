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
  <path d="M16,25.36c-10.411,0-14.295-9.131-14.333-9.223c-0.036-0.088-0.036-0.187,0-0.274	C1.705,15.771,5.589,6.64,16,6.64c10.41,0,14.295,9.13,14.333,9.223c0.036,0.088,0.036,0.187,0,0.274	C30.295,16.229,26.41,25.36,16,25.36z M2.395,16C2.916,17.117,6.771,24.64,16,24.64S29.084,17.118,29.605,16	C29.084,14.882,25.229,7.36,16,7.36S2.916,14.882,2.395,16z M16,23.36c-4.058,0-7.36-3.302-7.36-7.36S11.942,8.64,16,8.64	c4.059,0,7.36,3.302,7.36,7.36C23.36,20.059,20.059,23.36,16,23.36z M16,9.36c-3.661,0-6.64,2.979-6.64,6.64s2.979,6.64,6.64,6.64	s6.64-2.979,6.64-6.64S19.661,9.36,16,9.36z M16,19.86c-2.128,0-3.86-1.732-3.86-3.86s1.731-3.86,3.86-3.86	c2.128,0,3.86,1.731,3.86,3.86C19.86,18.128,18.128,19.86,16,19.86z M16,12.86c-1.731,0-3.14,1.409-3.14,3.14s1.409,3.14,3.14,3.14	s3.14-1.408,3.14-3.14S17.731,12.86,16,12.86z"></path>
</svg>