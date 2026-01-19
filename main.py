'''
Script to query genbank for unclassified virus sequences from user-defined parameters
@mayne941 19/01/25
'''

def generate_query(taxid, search_terms, length_range, date_range):
    '''Iteratively build genbank query from user parameters'''
    query_parts = []
    query_wildcards = ["NAME sp.", "unverified NAME", "unclassified NAME"]

    for name in search_terms:
        for idx, wildcard in enumerate(query_wildcards):
            if not idx == 0:
                query_parts.append('OR ')
            query_parts.append(f'"{wildcard.replace("NAME", name)}"[Organism] OR ("{wildcard.replace("NAME", name)}"[Organism] OR {wildcard.replace("NAME", name)}[All Fields])')

    '''If TaxID provided, add to query'''
    if len(taxid) > 0:
        query_parts.append(f'OR txid{taxid}[Organism:exp] ')

    '''Add length and date restrictions'''
    query_parts.append(f'AND (({length_range[0]}:{length_range[1]}[SLEN]) AND ("{date_range[0]}"[PDAT] : "{date_range[1]}"[PDAT]))')

    full_query = ' '.join(query_parts)
    return full_query

if __name__ == "__main__":
    '''Run as $ python3 -m gen_gb_query'''
    search_terms = ["orthoherpesviridae", "herpesviridae"] # INPUT YOUR SEARCH TERMS HERE
    taxid = "3065635"                                      # LEAVE AS EMPTY STRING -- i.e. "" -- IF NO TAXID REQUIRED
    length_range = (10, 300000)                            # INPUT YOUR LENGTH RANGE HERE AS (MIN, MAX)
    date_range = ("2023/01/01", "2026/12/31")              # INPUT YOUR DATE RANGE HERE AS (START_DATE, END_DATE)

    query = generate_query(taxid, search_terms, length_range, date_range)
    print(f"Generated GenBank Query:\n{query}")
