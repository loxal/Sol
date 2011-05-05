/*
 * Copyright 2010 Alexander Orlov <alexander.orlov@loxal.net>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

//TODO GWTize
function listObj(obj) {
	document.write('<h3>' + obj + ' Methods&amp;Properties</h3>')
	document.writeln('<dl>')
	for (var entity in obj) {
		switch (typeof obj[entity]) {
			case 'object':
					document.writeln('<dt>' + obj + '.' + entity + '(' + obj[entity] + ')' + '</dt>')
					document.writeln('<dd>')
					listArray(entity)
					document.writeln('</dd>')
				break;
			case 'function':
					document.writeln('<dt>' + obj + '.' + entity + '</dt>')
					// : display the actual value and not only the function name
					document.writeln('<dd>' + obj[entity] + '</dd>')
				break;
			default:
					document.writeln('<dt>' + obj + '.' + entity + '</dt>')
					document.writeln('<dd>' + obj[entity] + '</dd>')
				break;
		}
	}
	document.writeln('</dl>')
}

function listArray(array) {
	document.writeln('<ul>')
	for (var elem in array) {
		document.writeln('<li>' + elem + '</li>')
	}
	document.writeln('</ul>')
}

listObj(screen)
listObj(navigator)
