import constants as c
import geopandas as gpd
import os


# map files acquired from: https://datacatalog.worldbank.org/search/dataset/0038272/World-Bank-Official-Boundaries

def main():
    """
    main driver for processing maps and assigning GCAM regions
    :return: nothing, but yields shapefiles
    """
    # read data
    df = gpd.read_file(c.GCAMConstants.unprocessed_map_loc)

    # apply region labels
    df['GCAM'] = df.apply(lambda row: label_region(row), axis=1)

    # list of countries/islands/territories that are too small to be assigned to GCAM regions
    mistakes = df[df.GCAM == c.GCAMConstants.missing]

    # remove minor islands and such
    df = df.drop(df[df.GCAM == c.GCAMConstants.missing].index)

    #remove unnecessary columns
    df = df[c.GCAMConstants.world_columns]

    df.to_file(c.GCAMConstants.processed_map_loc)


def label_region(row):
    """
    matches a country name with GCAM region
    :param row: row in a dataframe
    :return: the GCAM regions, or if it is missing
    """
    if row['NAME_EN'] in ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Mauritius",
                          "Reunion", "Rwanda", "South Sudan", "Sudan", "Somalia", "Uganda", "Somaliland"]:
        return "Africa_Eastern"
    if row['NAME_EN'] in ["Algeria", "Egypt", "W. Sahara", "Libya", "Morocco", "Tunisia"]:
        return "Africa_Northern"
    if row['NAME_EN'] in ["Angola", "Botswana", "Lesotho", "Mozambique", "Malawi", "Namibia", "Swaziland", "Tanzania",
                          "Zambia", "Zimbabwe", "eSwatini"]:
        return "Africa_Southern"
    if row['NAME_EN'] in ["Benin", "Burkina Faso", "Central African Republic", "Ivory Coast", "Cameroon",
                          "Democratic Republic of the Congo", "Republic of the Congo", "Cape Verde", "Gabon", "Ghana",
                          "Guinea", "The Gambia", "Guinea-Bissau", "Eq. Guinea", "Liberia", "Mali", "Mauritania",
                          "Niger", "Nigeria", "Senegal", "Sierra Leone", "Sao Tome and Principe", "Chad", "Togo",
                          "Equatorial Guinea"]:
        return "Africa_Western"
    if row['NAME_EN'] in ['Argentina']:
        return "Argentina"
    if row['NAME_EN'] in ["Australia", 'New Zealand']:
        return "Australia_NZ"
    if row['NAME_EN'] in ["Brazil"]:
        return "Brazil"
    if row['NAME_EN'] in ["Canada"]:
        return "Canada"
    if row['NAME_EN'] in ["Aruba", "Anguilla", "Netherlands Antilles", "Antigua & Barbuda", "Bahamas", "Belize",
                          "Bermuda", "Barbados", "Costa Rica", "Cuba", "Cayman Islands", "Dominica",
                          "Dominican Republic", "Guadeloupe", "Grenada", "Guatemala", "Honduras", "Haiti", "Jamaica",
                          "Saint Kitts and Nevis", "Saint Lucia", "Montserrat", "Martinique", "Nicaragua", "Panama",
                          "El Salvador", "Trinidad and Tobago", "Saint Vincent and the Grenadines"]:
        return "Central America and Caribbean"
    if row['NAME_EN'] in ["Armenia", "Azerbaijan", "Georgia", "Kazakhstan", "Kyrgyzstan", "Mongolia", "Tajikistan",
                          "Turkmenistan", "Uzbekistan"]:
        return "Central Asia"
    if row['NAME_EN'] in ["People's Republic of China"]:
        return "China"
    if row['NAME_EN'] in ["Colombia"]:
        return "Colombia"
    if row['NAME_EN'] in ["Bulgaria", "Cyprus", "Czech Republic", "Estonia", "Hungary", "Lithuania", "Latvia", "Malta",
                          "Poland", "Romania", "Slovakia", "Slovenia", "N. Cyprus"]:
        return "EU-12"
    if row['NAME_EN'] in ["Andorra", "Austria", "Belgium", "Denmark", "Finland", "France", "Germany", "Greece",
                          "Greenland", "Ireland", "Italy", "Luxembourg", "Monaco", "Netherlands", "Portugal", "Sweden",
                          "Spain", "United Kingdom"]:
        return "EU-15"
    if row['NAME_EN'] in ["Belarus", "Moldova", "Ukraine"]:
        return "Europe_Eastern"
    if row['NAME_EN'] in ["Iceland", "Norway", "Switzerland"]:
        return "European Free Trade Association"
    if row['NAME_EN'] in ["Albania", "Bosnia and Herzegovina", "Croatia", "Republic of Macedonia", "Montenegro",
                          "Serbia", "Turkey", "North Macedonia", "Kosovo"]:
        return "Europe_Non_EU"
    if row['NAME_EN'] in ["India"]:
        return "India"
    if row['NAME_EN'] in ["Indonesia"]:
        return "Indonesia"
    if row['NAME_EN'] in ["Japan"]:
        return "Japan"
    if row['NAME_EN'] in ["Mexico"]:
        return "Mexico"
    if row['NAME_EN'] in ["United Arab Emirates", "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon",
                          "Oman", "Palestine", "Qatar", "Saudi Arabia", "Syria", "Yemen"]:
        return "Middle East"
    if row['NAME_EN'] in ["Pakistan"]:
        return "Pakistan"
    if row['NAME_EN'] in ["Russia"]:
        return "Russia"
    if row['NAME_EN'] in ["South Africa"]:
        return "South Africa"
    if row['NAME_EN'] in ["French Guiana", "Guyana", "Suriname", "Venezuela"]:
        return "South America_Northern"
    if row['NAME_EN'] in ["Bolivia", "Chile", "Ecuador", "Peru", "Paraguay", "Uruguay"]:
        return "South America_Southern"
    if row['NAME_EN'] in ["Afghanistan", "Bangladesh", "Bhutan", "Sri Lanka", "Maldives", "Nepal"]:
        return "South Asia"
    if row['NAME_EN'] in ["American Samoa", "Brunei", "Cocos (Keeling) Islands", "Cook Islands",
                          "Christmas Island", "Fiji", "Federated States of Micronesia", "Guam", "Cambodia", "Kiribati",
                          "Laos", "Marshall Islands", "Myanmar", "Northern Mariana Islands",
                          "Malaysia", "Mayotte", "New Caledonia", "Norfolk Island", "Niue", "Nauru",
                          "Pacific Islands Trust Territory", "Pitcairn Islands", "Philippines", "Palau",
                          "Papua New Guinea", "North Korea", "French Polynesia", "Singapore",
                          "Solomon Is.", "Seychelles", "Thailand", "Tokelau", "Timor-Leste", "Tonga", "Tuvalu",
                          "Vietnam", "Vanuatu", "Samoa", "East Timor"]:
        return "Southeast Asia"
    if row['NAME_EN'] in ["South Korea"]:
        return "South Korea"
    if row['NAME_EN'] in ["Taiwan"]:
        return "Taiwan"
    if row['NAME_EN'] in ['United States of America', "Puerto Rico"]:
        return "USA"
    return c.GCAMConstants.missing


if __name__ == '__main__':
    main()
