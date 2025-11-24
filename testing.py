import polyline
import folium

summary_polyline = "ctx|HyabFJJp@Ld@B^NbANLj@ShDa@xE?VB`CBNDjD@fDFjCA~BFbCA`AL~CCl@?lAM^_@d@{C|@Q`@A`AD`@^zC?PILc@Lc@KYR[JS\\aCp@eAx@a@NQLA\\hAhDdD|IjAlDpA|CfAlDRj@^t@Pl@j@tAVz@Xn@JL^|@NTnAlAtA`BNJn@~@p@lB`@|Aj@bBJp@`@X\\f@f@~AVrAPh@z@jBPr@Zx@p@pAN`@p@v@Hp@Jf@HJ~BvAtB|Av@b@dAXxBLt@EzA?tBJ~AAnAId@@l@Gd@F\\b@FXJp@?j@IHMfAGRYd@Of@a@z@Oz@Cr@Bj@XjAEV_@lAMn@AZQtD@z@IhAAxCBlCINaACy@MQSMWc@[y@a@i@I_@c@K|HI`@ED[BoAOmFWi@IS_@E]@mARsJDYTSdKn@LNBVIpE?x@MdEI`@MH{FQwAIi@KMSEW@gBHoCFgFDWPMrAJbH`@NJBHDZShMGXKLYDmCEwDUi@UIUA[FeHFmBFcADMTMP?tE^`CFPDLNBZKvEK~FGVKLQFo@AoHg@OEKSEYHyID}BH[DGLE~Ip@^DJLBf@WxHGlCMXeA@{Hg@MMI[@_BFiAHgHFYDIPId@?zDX~CVLLFTCjCU~HKb@s@FaDMcBEsAQOQCW@iCNsHBYJY^EbHXjANJNDVAdBMzFClBGVOPO@{HYs@MOQGWJqJFoBHYPGN?vBNfDJ~@NNDLNFZ@j@]bLO\\GDk@?uH]WEMOEYAiADcEJeE@MLUNET?`CPxCH`ALTPDV@ZUhLAXEJEFOFcGUoBSOGEIGW?k@PkK@g@HWVOd@@fAN`BBlDZRXBZM~DKhGM^QFaCAsFe@OMGWA]ViMJSFCpDNd@AlDVLRDZGhDdC`@j@~@XXtATNCRMG}@EcDBsBLkDRcCd@}BA_@SgACa@@OXg@NyANe@Zo@\\sARg@QsAGUISGoDU}BUsACu@JgAJYRsHLgCDYJ}D?qBG_ARiICiCUsDEqCLm@Bc@?iAGs@GOUUYOa@MkAMc@UOSQq@UUm@WWYCWPaAn@iCLq@@aAOUW_CQk@GuAM_ACy@A}@H_C@y@CwAJaFCeBBiALm@AoBFORy@FqBGkACgBMa@?_AKq@UYe@[SSWK{@Eq@Ss@CeA[e@YeA}@UWISaA}@m@w@s@k@cK_B}Ae@_Du@sC[gDq@eCYkAWOISk@"
coords = polyline.decode(summary_polyline)
map = folium.Map(location=coords[0], zoom_start=30)
folium.PolyLine(coords, weight=5).add_to(map)
map_html = map._repr_html_()

print(map_html)

